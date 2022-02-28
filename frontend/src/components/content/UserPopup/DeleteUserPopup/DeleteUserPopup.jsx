import React, { useEffect, useState } from "react";
import Popup from "../../../shared/interaction/Popup/Popup";
import Button from "@mui/material/Button";
import { Typography } from "@mui/material";
import * as Style from "./style";
import { useDispatch, useSelector } from "react-redux";
import { deleteUser } from "./../../../../redux/slices/userSlice";
import { useSnackbar } from "notistack";
import { alertGenericErrors } from "../../../../services/errorMessagesService"

function DeleteUserPopup({ OnActionClose }) {
  const [trigger, setTrigger] = useState(true);

  useEffect(() => {
    if (trigger === false) {
      if (OnActionClose instanceof Function) {
        OnActionClose();
      }
    }
  }, [trigger]);

  const snackBar = useSnackbar();
  const dispatch = useDispatch();
  const selectedUser = useSelector((state) => state.user.selectedUser);

  const OnDeleteHandler = (e) => {
    dispatch(deleteUser(selectedUser.id))
      .unwrap()
      .then(() => {
        snackBar.enqueueSnackbar("User Deleted Succesfully!", {
          variant: "success",
        });
        setTrigger(false);
        OnActionClose();
      }).catch((payload) => {
        alertGenericErrors(payload, snackBar);
      });
  };

  return (
    <Popup title="Delete User" trigger={trigger} setTrigger={setTrigger}>
      <Style.PopupContainer>
        <Typography variant="h6" display="block">
          Are you sure you want to delete
          <br /> this user?
        </Typography>
        <Style.ButtonContainer>
          <Button variant="contained" onClick={OnDeleteHandler}>
            Yes
          </Button>
          <Button variant="contained" onClick={OnActionClose}>Cancel</Button>
        </Style.ButtonContainer>
      </Style.PopupContainer>
    </Popup>
  );
}

export default DeleteUserPopup;
