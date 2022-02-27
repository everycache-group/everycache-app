import * as Style from "./style";
import React, { useState } from "react";
import { useSelector } from "react-redux";
import useForm from "./../../../hooks/useForm";
import Box from '@mui/material/Box';
import LoadingButton from "@mui/lab/LoadingButton";
import SendIcon from "@mui/icons-material/Send";
import {prepareErrors} from "../../../services/errorMessagesService"

function CommentForm({ Comment, OnFormSubmit, ButtonName }) {
  const { text } = Comment;
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
      text
    },
    () => {
      if (OnFormSubmit instanceof Function) {
        OnFormSubmit(formValues, setErrors);
      }
    }
  );


  return <Style.CommentFormWrapper>
            <Style.CommentTextField
              id="text"
              label="Comment"
              onChange={handleUserInput}
              name="text"
              error={!!errors.text}
              value={formValues.text}
              helperText={prepareErrors(errors.text)}
              placeholder="Enter comment text here..."
            />
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
          </Style.CommentFormWrapper>
}


export default CommentForm;
