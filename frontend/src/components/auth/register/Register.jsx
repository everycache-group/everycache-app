import React, { useState } from "react";
import * as Style from "./style";
import TextField from "@mui/material/TextField";
import LoadingButton from "@mui/lab/LoadingButton";
import useForm from "../../../hooks/useForm";
import { createUser } from "./../../../redux/slices/userSlice";
import { useDispatch } from "react-redux";
import { create } from "../../../api/api-core";
import { alertGenericErrors, prepareErrors, alertFormErrors } from "../../../services/errorMessagesService"
import { useSnackbar } from "notistack";

function Register() {
  const [registering, setRegistering] = useState(false);

  const dispatch = useDispatch();
  const snackBar = useSnackbar();

  const { handleFormSubmit, handleUserInput, formValues, errors, setErrors } = useForm(
    {
      username: "",
      email: "",
      password: "",
      password2: "",
    },
    () => {
      const { username, email, password } = formValues;

      if(formValues.password !== formValues.password2) {
        setErrors({password2: ["Passwords should match!"]});
      }
      else{
        dispatch( createUser({
            username,
            email,
            password,
          })
        )
        .unwrap()
        .then(()=>{})
        .catch((payload) => {
            alertFormErrors(payload, setErrors);
            alertGenericErrors(payload, snackBar);
        });
      }

    }
  );

  return (
    <div>
      <Style.RegisterForm>
        <TextField
          size="small"
          id="username"
          error={!!errors.username}
          helperText={prepareErrors(errors.username)}
          onChange={handleUserInput}
          type="username"
          name="username"
          label="Username"
        />
        <TextField
          size="small"
          id="email"
          error={!!errors.email}
          helperText={prepareErrors(errors.email)}
          onChange={handleUserInput}
          type="email"
          name="email"
          label="Email"
        />
        <TextField
          size="small"
          id="password"
          error={!!errors.password}
          helperText={prepareErrors(errors.password)}
          onChange={handleUserInput}
          type="password"
          name="password"
          label="Password"
        />
        <TextField
          size="small"
          id="password2"
          error={!!errors.password2}
          helperText={prepareErrors(errors.password2)}
          onChange={handleUserInput}
          type="password"
          name="password2"
          label="Repeat Password"
        />

        <LoadingButton
          onClick={handleFormSubmit}
          loading={registering}
          variant="contained"
          color="success"
          type="submit"
        >
          Register
        </LoadingButton>
      </Style.RegisterForm>
    </div>
  );
}

export default Register;
