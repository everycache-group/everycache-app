import React, { useState, useEffect } from "react";
import Popup from "./../../../shared/interaction/Popup/Popup";
import CacheForm from "../../cacheForm/CacheForm";
import { createCache } from "./../../../../redux/slices/cacheSlice";
import { useDispatch, useSelector } from "react-redux";
import { useSnackbar } from "notistack";
import { alertFormErrors, alertGenericErrors } from "../../../../services/errorMessagesService"
import CommentForm from "../../commentForm/CommentForm"
import { addComment } from "../../../../redux/slices/commentSlice"

function AddCommentPopup({ OnActionClose }) {
  const dispatch = useDispatch();
  const snackBar = useSnackbar();
  const [trigger, setTrigger] = useState(true);
  const selectedCache = useSelector((state) => state.cache.selectedCache);

  useEffect(() => {
    if (trigger === false) {
      if (OnActionClose instanceof Function) {
        OnActionClose();
      }
    }
  }, [trigger]);

  const OnFormSubmitHandler = (formData, setErrors) => {
    const createCommentDto = {
      cacheId: selectedCache.id,
      text: formData.text
    };

    dispatch(addComment(createCommentDto))
      .unwrap()
      .then(() => {
        snackBar.enqueueSnackbar("Comment Added Succesfully!", {
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
        Comment={{
          text: ""
        }}
        OnFormSubmit={OnFormSubmitHandler}
        ButtonName="Create"
      />
    </Popup>
  );
}

export default AddCommentPopup;
