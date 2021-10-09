import React from "react";
import * as Style from "./style";
import Register from "../../components/auth/register/Register";
import Login from "../../components/auth/login/Login";

function AuthenticationPage() {
  return (
    <Style.AuthWrapper>
      <Style.AuthContainer>
        <Login />
      </Style.AuthContainer>
    </Style.AuthWrapper>
  );
}

export default AuthenticationPage;
