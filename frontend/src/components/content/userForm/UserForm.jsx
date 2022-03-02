import * as Style from "./style";
import React, { useState } from "react";
import { useSelector } from "react-redux";
import useForm from "./../../../hooks/useForm";
import Box from '@mui/material/Box';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';
import FormHelperText from '@mui/material/FormHelperText';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import LoadingButton from "@mui/lab/LoadingButton";
import SendIcon from "@mui/icons-material/Send";
import {prepareErrors} from "../../../services/errorMessagesService"

function UserForm({ User, OnFormSubmit, ButtonName }) {
  const { username, role, email, verified } = User;
  const [loading, setLoading] = useState(false);

  const selectedUser = useSelector((state) => state.user.selectedUser);
  const currentUserRole = useSelector((state) => state.user.role);
  const currentUserId = useSelector((state) => state.user.id);

  const {
    handleFormSubmit,
    handleUserInput,
    formValues,
    errors,
    setFormValues,
    setErrors
  } = useForm(
    {
      username,
      role,
      email,
      verified
    },
    () => {
      if (OnFormSubmit instanceof Function) {
        OnFormSubmit(formValues, setErrors);
      }
    }
  );


  return <Style.UserFormWrapper>
            <Style.UserTextField
              id="username"
              label="Username"
              onChange={handleUserInput}
              name="username"
              error={!!errors.username}
              helperText={prepareErrors(errors.username)}
              placeholder="Enter Username Here..."
              value={formValues.username}
            />
            <Style.UserTextField
              id="email"
              label="Email"
              onChange={handleUserInput}
              name="email"
              error={!!errors.email}
              helperText={prepareErrors(errors.email)}
              placeholder="Enter email Here..."
              value={formValues.email}
              disabled={currentUserRole != "Admin"}
            />

            <Style.UserTextField
              id="password"
              label="Password"
              onChange={handleUserInput}
              name="password"
              type="password"
              error={!!errors.password}
              helperText={prepareErrors(errors.password)}
              placeholder="Enter password Here..."
            />

            {currentUserId == selectedUser.id && <Style.UserTextField
              id="current_password"
              label="Current Password"
              onChange={handleUserInput}
              name="current_password"
              type="password"
              error={!!errors.current_password}
              helperText={prepareErrors(errors.current_password)}
              placeholder="Enter current password Here..."
            />}

            {currentUserRole == "Admin" && (<Style.SelectWrapper>
              <Style.UserFormControl fullWidth>
                <InputLabel id="roleL">Role</InputLabel>
                <Select
                  labelId="roleL"
                  id="role"
                  name="role"
                  value={formValues.role}
                  label="Role"
                  onChange={handleUserInput}
                >
                  <MenuItem value={"Default"}>Default</MenuItem>
                  <MenuItem value={"Admin"}>Admin</MenuItem>
                </Select>
              </Style.UserFormControl>

              <Style.UserFormControl fullWidth>
                <InputLabel id="verifiedL">Verified</InputLabel>
                <Select
                  labelId="verifiedL"
                  id="verified"
                  name="verified"
                  value={formValues.verified}
                  label="verified"
                  onChange={handleUserInput}
                >
                  <MenuItem value={"false"}>Not Verified</MenuItem>
                  <MenuItem value={"true"}>Verified</MenuItem>
                </Select>
              </Style.UserFormControl>
            </Style.SelectWrapper>)}
            <LoadingButton
              onClick={handleFormSubmit}
              endIcon={<SendIcon />}
              loadingPosition="end"
              loading={loading}
              variant="contained"
              color="success"
              type="submit"
            >
              {ButtonName}
            </LoadingButton>
          </Style.UserFormWrapper>
}


export default UserForm;
