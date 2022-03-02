import React, { useState, useEffect } from "react";
import Popup from "./../../../shared/interaction/Popup/Popup";
import CacheForm from "../../cacheForm/CacheForm";
import { updateCache } from "./../../../../redux/slices/cacheSlice";
import { useDispatch, useSelector } from "react-redux";
import { selector } from "react-redux";
import { useSnackbar } from "notistack";
import { alertGenericErrors, alertFormErrors } from "../../../../services/errorMessagesService"

function EditCachePopup({ OnActionClose }) {
  const [trigger, setTrigger] = useState(true);

  const selectedCache = useSelector((state) => state.cache.selectedCache);

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
    console.log(selectedCache.id);
    const updateCacheDto = {
      id: selectedCache.id,
      description: formData.description,
      lat: formData.lat,
      lon: formData.lon,
      name: formData.name,
    };

    dispatch(updateCache(updateCacheDto))
      .unwrap()
      .then(() => {
        snackBar.enqueueSnackbar("Cache Updated Succesfully!,", {
          variant: "info",
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
      <CacheForm
        Cache={selectedCache}
        OnFormSubmit={OnFormSubmitHandler}
        ButtonName="Update"
      />
    </Popup>
  );
}

export default EditCachePopup;
