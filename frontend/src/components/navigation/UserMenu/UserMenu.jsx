import DeleteIcon from "@mui/icons-material/Delete";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import EditIcon from "@mui/icons-material/Edit";
import { useSelector } from "react-redux";
import React, { useState } from "react";
import { useSnackbar } from "notistack";
import * as Style from "./style";
import EditUserPopup from "./../../content/UserPopup/EditUserPopup/EditUserPopup";
import DeleteUserPopup from "./../../content/UserPopup/DeleteUserPopup/DeleteUserPopup";

function UserMenu() {
  const [action, setAction] = useState("");

  const selectedUser = useSelector((state) => state.user.selectedUser);
  const snackBar = useSnackbar();

  const OnClickHandler = (e) => {
    if (selectedUser){
      setAction(e.currentTarget.id);
    }
    else{
      snackBar.enqueueSnackbar("No user selected for action!", {variant: "error"});
    }
  };

  const OnActionClose = () => {
    setAction("");
  };

  return (
    <Style.UserActionContainer>
      <div onClick={OnClickHandler} id="edit">
        <Style.TransformIconButton aria-label="Edit User">
          <EditIcon fontSize="medium" color="info" />
        </Style.TransformIconButton>
        {action === "edit" && <EditUserPopup OnActionClose={OnActionClose} />}
      </div>
      <div onClick={OnClickHandler} id="delete">
        <Style.TransformIconButton aria-label="Delete User">
          <DeleteIcon fontSize="medium" color="error" />
        </Style.TransformIconButton>
        {action === "delete" && (
          <DeleteUserPopup OnActionClose={OnActionClose} />
        )}
      </div>
    </Style.UserActionContainer>
  );
}

export default UserMenu;
