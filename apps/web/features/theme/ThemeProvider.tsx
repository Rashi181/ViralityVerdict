"use client";

import html2canvas from "html2canvas";
import { gsap } from "gsap";
import { createContext, type ReactNode, useCallback, useContext, useEffect, useRef, useState } from "react";

type Theme = "light" | "dark";
type ThemeContextValue = { theme: Theme; toggleTheme: (origin?: { x: number; y: number }) => void };
const ThemeContext = createContext<ThemeContextValue | null>(null);
const key = "verdict-theme";

function preferredTheme(): Theme {
  return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

function apply(theme: Theme) {
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
  window.localStorage.setItem(key, theme);
}

function farthestCorner({ x, y }: { x: number; y: number }) {
  const { innerWidth: width, innerHeight: height } = window;
  return Math.max(Math.hypot(x, y), Math.hypot(width - x, y), Math.hypot(x, height - y), Math.hypot(width - x, height - y)) + 24;
}

function playCanvasInkFallback(snapshot: HTMLCanvasElement, origin: { x: number; y: number }) {
  const overlay = document.createElement("canvas");
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  const width = window.innerWidth;
  const height = window.innerHeight;
  overlay.width = Math.round(width * ratio);
  overlay.height = Math.round(height * ratio);
  overlay.className = "ink-reveal-overlay";
  document.body.append(overlay);

  const context = overlay.getContext("2d");
  if (!context) {
    overlay.remove();
    return;
  }

  const seed = Math.random() * Math.PI * 2;
  const maxRadius = farthestCorner(origin);
  const state = { progress: 0 };
  const draw = () => {
    const radius = Math.max(1, state.progress * maxRadius);
    context.save();
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    context.clearRect(0, 0, width, height);
    context.drawImage(snapshot, 0, 0, width, height);
    context.globalCompositeOperation = "destination-out";
    context.beginPath();
    for (let step = 0; step <= 96; step += 1) {
      const angle = (step / 96) * Math.PI * 2;
      const wobble = 1 + 0.1 * Math.sin(angle * 5 + seed) + 0.055 * Math.sin(angle * 11 - seed * 1.7);
      const x = origin.x + Math.cos(angle) * radius * wobble;
      const y = origin.y + Math.sin(angle) * radius * wobble;
      if (step === 0) context.moveTo(x, y);
      else context.lineTo(x, y);
    }
    context.closePath();
    context.fill();
    context.restore();
  };

  draw();
  return gsap.to(state, {
    progress: 1.34,
    duration: 2.15,
    ease: "power3.out",
    onUpdate: draw,
    onComplete: () => overlay.remove(),
  });
}

const vertexShader = `#version 300 es
in vec2 position;
in vec2 texCoord;
out vec2 uv;
void main() {
  uv = texCoord;
  gl_Position = vec4(position, 0.0, 1.0);
}`;

// The expanding edge is generated on the GPU: layered value noise creates the uneven,
// liquid boundary and small leading droplets rather than a geometric circular wipe.
const fragmentShader = `#version 300 es
precision highp float;
uniform sampler2D source;
uniform vec2 origin;
uniform float progress;
uniform float time;
out vec4 outputColor;

float hash(vec2 point) { return fract(sin(dot(point, vec2(127.1, 311.7))) * 43758.5453123); }
float noise(vec2 point) {
  vec2 cell = floor(point);
  vec2 local = fract(point);
  vec2 curve = local * local * (3.0 - 2.0 * local);
  return mix(mix(hash(cell), hash(cell + vec2(1.0, 0.0)), curve.x), mix(hash(cell + vec2(0.0, 1.0)), hash(cell + vec2(1.0, 1.0)), curve.x), curve.y);
}
float fbm(vec2 point) {
  float result = 0.0;
  float weight = 0.56;
  for (int layer = 0; layer < 4; layer++) {
    result += weight * noise(point);
    point = point * 2.07 + 8.31;
    weight *= 0.5;
  }
  return result;
}
void main() {
  vec2 scale = vec2(1.0, 1.0);
  vec2 delta = (uv - origin) * scale;
  float distanceToInk = length(delta);
  float inkRadius = progress * 1.46;
  float broadGrain = (fbm(uv * 3.2 + time * 0.045) - 0.5) * (0.28 - min(progress, 1.0) * 0.105);
  float fineGrain = (fbm(uv * 15.0 - time * 0.11) - 0.5) * 0.045;
  float mainEdge = smoothstep(inkRadius - 0.04, inkRadius + 0.048, distanceToInk + broadGrain + fineGrain);

  // A sparse set of faster, noisy droplets gives the boundary its spilled-ink character.
  float droplets = 1.0;
  for (int index = 0; index < 28; index++) {
    float id = float(index);
    float angle = hash(vec2(id, 4.1)) * 6.2831853;
    float lead = 0.32 + hash(vec2(id, 9.7)) * 0.92;
    vec2 center = origin + vec2(cos(angle), sin(angle)) * inkRadius * lead;
    float size = (0.01 + hash(vec2(id, 2.3)) * 0.042) * smoothstep(0.08, 0.72, progress);
    float drop = 1.0 - smoothstep(size * 0.66, size, length(uv - center));
    droplets *= 1.0 - drop * smoothstep(0.1, 0.86, progress);
  }

  vec4 oldPage = texture(source, uv);
  outputColor = vec4(oldPage.rgb, oldPage.a * mainEdge * droplets);
}`;

function makeProgram(gl: WebGL2RenderingContext) {
  const compile = (type: number, source: string) => {
    const shader = gl.createShader(type);
    if (!shader) return null;
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    return gl.getShaderParameter(shader, gl.COMPILE_STATUS) ? shader : null;
  };
  const vertex = compile(gl.VERTEX_SHADER, vertexShader);
  const fragment = compile(gl.FRAGMENT_SHADER, fragmentShader);
  if (!vertex || !fragment) return null;
  const program = gl.createProgram();
  if (!program) return null;
  gl.attachShader(program, vertex);
  gl.attachShader(program, fragment);
  gl.linkProgram(program);
  gl.deleteShader(vertex);
  gl.deleteShader(fragment);
  return gl.getProgramParameter(program, gl.LINK_STATUS) ? program : null;
}

function playInkReveal(snapshot: HTMLCanvasElement, origin: { x: number; y: number }) {
  const overlay = document.createElement("canvas");
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  const width = window.innerWidth;
  const height = window.innerHeight;
  overlay.width = Math.round(width * ratio);
  overlay.height = Math.round(height * ratio);
  overlay.className = "ink-reveal-overlay";
  document.body.append(overlay);

  const gl = overlay.getContext("webgl2", { alpha: true, antialias: false, premultipliedAlpha: false });
  if (!gl) {
    overlay.remove();
    return playCanvasInkFallback(snapshot, origin);
  }
  const program = makeProgram(gl);
  if (!program) {
    overlay.remove();
    return playCanvasInkFallback(snapshot, origin);
  }

  const geometry = gl.createBuffer();
  const texture = gl.createTexture();
  if (!geometry || !texture) {
    overlay.remove();
    return playCanvasInkFallback(snapshot, origin);
  }
  gl.bindBuffer(gl.ARRAY_BUFFER, geometry);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
    -1, -1, 0, 0, 1, -1, 1, 0, -1, 1, 0, 1, 1, 1, 1, 1,
  ]), gl.STATIC_DRAW);
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, snapshot);

  const position = gl.getAttribLocation(program, "position");
  const texCoord = gl.getAttribLocation(program, "texCoord");
  const source = gl.getUniformLocation(program, "source");
  const originUniform = gl.getUniformLocation(program, "origin");
  const progressUniform = gl.getUniformLocation(program, "progress");
  const timeUniform = gl.getUniformLocation(program, "time");
  const state = { progress: 0 };
  const start = performance.now();
  const draw = () => {
    gl.viewport(0, 0, overlay.width, overlay.height);
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.useProgram(program);
    gl.bindBuffer(gl.ARRAY_BUFFER, geometry);
    gl.enableVertexAttribArray(position);
    gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 16, 0);
    gl.enableVertexAttribArray(texCoord);
    gl.vertexAttribPointer(texCoord, 2, gl.FLOAT, false, 16, 8);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.uniform1i(source, 0);
    gl.uniform2f(originUniform, origin.x / width, 1 - origin.y / height);
    gl.uniform1f(progressUniform, state.progress);
    gl.uniform1f(timeUniform, (performance.now() - start) / 1000);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  };

  draw();
  return gsap.to(state, {
    progress: 1.3,
    duration: 2.35,
    ease: "power3.out",
    onUpdate: draw,
    onComplete: () => {
      gl.deleteBuffer(geometry);
      gl.deleteTexture(texture);
      gl.deleteProgram(program);
      overlay.remove();
    },
  });
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>("dark");
  const initialThemeFrame = useRef<number | null>(null);

  useEffect(() => {
    const saved = window.localStorage.getItem(key);
    const next = saved === "light" || saved === "dark" ? saved : preferredTheme();
    apply(next);
    initialThemeFrame.current = window.requestAnimationFrame(() => {
      initialThemeFrame.current = null;
      setTheme(next);
    });
    return () => {
      if (initialThemeFrame.current !== null) window.cancelAnimationFrame(initialThemeFrame.current);
    };
  }, []);

  const toggleTheme = useCallback((origin?: { x: number; y: number }) => {
    if (initialThemeFrame.current !== null) {
      window.cancelAnimationFrame(initialThemeFrame.current);
      initialThemeFrame.current = null;
    }
    const next: Theme = document.documentElement.dataset.theme === "light" ? "dark" : "light";
    const change = () => {
      apply(next);
      setTheme(next);
    };
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) {
      change();
      return;
    }

    const point = origin ?? { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    // Keep a painted copy of the outgoing page above the new theme, then erase
    // it with the uneven canvas/WebGL ink edge. This is deliberately not a
    // circular CSS reveal: the spill originates from the switch itself.
    void html2canvas(document.documentElement, {
      backgroundColor: null,
      logging: false,
      scale: Math.min(window.devicePixelRatio || 1, 2),
      width: window.innerWidth,
      height: window.innerHeight,
      windowWidth: window.innerWidth,
      windowHeight: window.innerHeight,
    }).then((snapshot) => {
      change();
      playInkReveal(snapshot, point);
    }).catch(change);
  }, []);

  return <ThemeContext.Provider value={{ theme, toggleTheme }}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const value = useContext(ThemeContext);
  if (!value) throw new Error("useTheme must be used inside ThemeProvider");
  return value;
}
