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
    console.log("SUBMIT")
    const updateUserDto = {
      id: selectedUser.id,
      username: formData.username,
      role: formData.role,
      email: formData.email,
      verified: formData.verified,
    };

    dispatch(updateUser(updateUserDto)).then(({ meta }) => {
      snackBar.enqueueSnackbar("User Updated Succesfully!", {
        variant: "success",
      });
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
