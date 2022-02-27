import React, { useState, useEffect } from "react";
import Popup from "./../../../shared/interaction/Popup/Popup";
import CacheForm from "../../cacheForm/CacheForm";
import { createCache } from "./../../../../redux/slices/cacheSlice";
import { useDispatch, useSelector } from "react-redux";
import { useSnackbar } from "notistack";
import { alertFormErrors, alertGenericErrors } from "../../../../services/errorMessagesService"
import CommentForm from "../../commentForm/CommentForm"
import { updateComment } from "../../../../redux/slices/commentSlice"

function EditCommentPopup({ OnActionClose, Comment }) {
  const dispatch = useDispatch();
  const snackBar = useSnackbar();
  const [trigger, setTrigger] = useState(true);

  useEffect(() => {
    if (trigger === false) {
      if (OnActionClose instanceof Function) {
        OnActionClose();
      }
    }
  }, [trigger]);

  const OnFormSubmitHandler = (formData, setErrors) => {
    const editCommentDto = {
      id: Comment.id,
      text: formData.text
    };

    dispatch(updateComment(editCommentDto))
      .unwrap()
      .then(() => {
        snackBar.enqueueSnackbar("Comment Updated Succesfully!", {
          variant: "success",
        });
        setTrigger(false);
        OnActionClose();
      })
      .catch((payload) => {
        alertFormErrors(payload, setErrors);
        alertGenericErrors(payload, snackBar);
      });
  };

  return (
    <Popup trigger={trigger} setTrigger={setTrigger}>
      <CommentForm
        Comment={Comment}
        OnFormSubmit={OnFormSubmitHandler}
        ButtonName="Update"
      />
    </Popup>
  );
}

export default EditCommentPopup;
