import React, { useState } from "react";
import * as Style from "./style";
import TextField from "@mui/material/TextField";
import LoadingButton from "@mui/lab/LoadingButton";
import useForm from "../../../hooks/useForm";
import * as auth from "../../../services/authService";
import { login } from "./../../../redux/slices/authSlice";
import { useDispatch } from "react-redux";
import { Redirect } from "react-router";

function Login() {
  const [registering, setRegistering] = useState(false);
  const [redirect, setRedirect] = useState(false);

  const dispatch = useDispatch();

  const { handleFormSubmit, handleUserInput, formValues, errors } = useForm(
    {
      email: "",
      password: "",
    },
    () => {
      const { email, password } = formValues;

      auth
        .loginUser(email, password, (response) => {
          dispatch(
            login({
              access_token: response.access_token,
              refresh_token: response.refresh_token,
            })
          );

          setRedirect(true);
        })
        .catch((x) => console.log(x));
    }
  );

  if (redirect) return <Redirect to="/" />;

  return (
    <Style.LoginForm>
      <TextField
        size="small"
        id="email"
        error={!!errors.email}
        helperText={errors.email}
        onChange={handleUserInput}
        type="email"
        name="email"
        label="Email"
      />
      <TextField
        size="small"
        id="password"
        error={!!errors.password}
        helperText={errors.password}
        onChange={handleUserInput}
        type="password"
        name="password"
        label="Password"
      />

      <LoadingButton
        onClick={handleFormSubmit}
        loading={registering}
        variant="contained"
        color="success"
      >
        Log in
      </LoadingButton>
    </Style.LoginForm>
  );
}

export default Login;
