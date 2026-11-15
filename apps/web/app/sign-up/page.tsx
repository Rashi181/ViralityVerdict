import { Suspense } from "react";
import { AuthForm } from "../../features/auth/AuthForm";

export default function SignUpPage() {
  return (
    <main id="main-content" className="auth-page" tabIndex={-1}>
      <Suspense fallback={null}>
        <AuthForm mode="sign-up" />
      </Suspense>
    </main>
  );
}
