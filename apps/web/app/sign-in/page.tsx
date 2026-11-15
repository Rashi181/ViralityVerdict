import { Suspense } from "react";
import { AuthForm } from "../../features/auth/AuthForm";

export default function SignInPage() {
  return (
    <main id="main-content" className="auth-page" tabIndex={-1}>
      <Suspense fallback={null}>
        <AuthForm mode="sign-in" />
      </Suspense>
    </main>
  );
}
