import React from "react";
import * as Style from "./style";
import Register from "../../components/auth/register/Register";
import Login from "../../components/auth/login/Login";
import { Redirect } from "react-router";
import { useSelector } from "react-redux";

function AuthenticationPage() {
  const logged = useSelector((state) => state.auth.logged);

  if (logged) return <Redirect to="/" />;

  return (
    <Style.AuthWrapper>
      <Style.AuthContainer>
        <Register />
      </Style.AuthContainer>
    </Style.AuthWrapper>
  );
}

export default AuthenticationPage;
