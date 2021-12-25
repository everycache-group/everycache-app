import React, { useState } from "react";
import * as Style from "./style";
import TextField from "@mui/material/TextField";
import LoadingButton from "@mui/lab/LoadingButton";
import useForm from "../../../hooks/useForm";
import { loginUser } from "./../../../redux/slices/authSlice";
import { useDispatch, useSelector } from "react-redux";

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
      dispatch(loginUser({ email, password }));
    }
  );

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
