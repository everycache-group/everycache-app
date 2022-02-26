import React, { useState } from "react";
import * as Style from "./style";
import TextField from "@mui/material/TextField";
import LoadingButton from "@mui/lab/LoadingButton";
import useForm from "../../../hooks/useForm";
import { loginUser } from "./../../../redux/slices/authSlice";
import { getUser } from "./../../../redux/slices/userSlice";
import { useDispatch, useSelector } from "react-redux";
import { useSnackbar } from "notistack";

function Login() {
  const [registering, setRegistering] = useState(false);

  const dispatch = useDispatch();
  const snackBar = useSnackbar();

  const { handleFormSubmit, handleUserInput, formValues, errors } = useForm(
    {
      email: "",
      password: "",
    },
    () => {
      const { email, password } = formValues;
      dispatch(loginUser({ email, password }))
        .unwrap()
        .then((result) => {
          const {userId} = result;
          dispatch(getUser(userId));
        })
        .catch((rejectedResult) => {
          snackBar.enqueueSnackbar("Invalid Email or Password. Try Again,", {
            variant: "error",
          });
        });
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
        type="submit"
      >
        Log in
      </LoadingButton>
    </Style.LoginForm>
  );
}

export default Login;
