import React, {useEffect} from 'react';
import { useRedirectFunctions } from "@propelauth/react";

function RegisterPage() {
  const { redirectToSignupPage } = useRedirectFunctions();
  
  useEffect(() => {
    redirectToSignupPage({ postSignupRedirectUrl: "http://localhost:3000" });
  }, [redirectToSignupPage]);

  return <div>Redirecting to signup...</div>;
}

export default RegisterPage;
