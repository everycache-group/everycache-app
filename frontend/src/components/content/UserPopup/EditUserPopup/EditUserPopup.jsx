import React, { useState, useEffect } from "react";
import Popup from "./../../../shared/interaction/Popup/Popup";
import UserForm from "../../userForm/UserForm";
import { updateUser } from "./../../../../redux/slices/userSlice";
import { useDispatch, useSelector } from "react-redux";
import { selector } from "react-redux";
import { useSnackbar } from "notistack";

function EditUserPopup({ OnActionClose }) {
  const [trigger, setTrigger] = useState(true);

  const selectedUser = useSelector((state) => state.user.selectedUser);
  const currentUserRole = useSelector((state) => state.user.role)

  const snackBar = useSnackbar();
  const dispatch = useDispatch();

  useEffect(() => {
    if (trigger === false) {
      if (OnActionClose instanceof Function) {
        OnActionClose();
      }
    }
  }, [trigger]);



  const OnFormSubmitHandler = (formData) => {
    let updateUserDto = {
      id: selectedUser.id,
      username: formData.username,
      email: formData.email,
    };

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

    dispatch(updateUser(updateUserDto)).then(({ meta }) => {
      const {requestStatus} = meta;
      console.log(meta);
      if (requestStatus == "fulfilled"){
        snackBar.enqueueSnackbar("User Updated Succesfully!", {
          variant: "success",
        });
      }
      else {
        snackBar.enqueueSnackbar("User Update has Failed!", {
          variant: "error",
        });
      }
      setTrigger(false);
      OnActionClose();
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
