import React, { useState, useEffect } from "react";
import Popup from "./../../../shared/interaction/Popup/Popup";
import UserForm from "../../userForm/UserForm";
import { updateUser } from "./../../../../redux/slices/userSlice";
import { useDispatch, useSelector } from "react-redux";
import { selector } from "react-redux";
import { useSnackbar } from "notistack";
import { alertGenericErrors, alertFormErrors } from "../../../../services/errorMessagesService"

function EditUserPopup({ OnActionClose }) {
  const [trigger, setTrigger] = useState(true);

  const selectedUser = useSelector((state) => state.user.selectedUser);
  const currentUserRole = useSelector((state) => state.user.role)
  const currentUserId = useSelector((state) => state.user.id)

  const snackBar = useSnackbar();
  const dispatch = useDispatch();

  useEffect(() => {
    if (trigger === false) {
      if (OnActionClose instanceof Function) {
        OnActionClose();
      }
    }
  }, [trigger]);



  const OnFormSubmitHandler = (formData, setErrors) => {
    let updateUserDto = {
      id: selectedUser.id,
      username: formData.username,
      email: formData.email,
    };

    if (formData.current_password) {
      updateUserDto["current_password"] = formData.current_password
    }

    if (currentUserRole == "Admin"){
      updateUserDto = {
        ...updateUserDto,
        role: formData.role,
        verified: formData.verified
      };
    }

    if ("password" in formData) {
      updateUserDto["password"] = formData.password;
    }

    dispatch(updateUser(updateUserDto)).unwrap().then((result) => {
      snackBar.enqueueSnackbar("User Updated Succesfully!", {
        variant: "success",
      });
      OnActionClose();
      setTrigger(false);
    }).catch((payload) => {
      alertFormErrors(payload, setErrors);
      alertGenericErrors(payload, snackBar);
    });
  };

  return (
      <Popup trigger={trigger} setTrigger={setTrigger}>
        <UserForm
          User={selectedUser}
          OnFormSubmit={OnFormSubmitHandler}
          ButtonName="Update"
        />
      </Popup>
  );
}

export default EditUserPopup;
