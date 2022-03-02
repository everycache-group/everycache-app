import React, { useState, useEffect } from "react";
import Popup from "./../../../shared/interaction/Popup/Popup";
import CacheForm from "../../cacheForm/CacheForm";
import { createCache, clearSelection } from "./../../../../redux/slices/cacheSlice";
import { useDispatch, useSelector } from "react-redux";
import { useSnackbar } from "notistack";
import { alertFormErrors, alertGenericErrors } from "../../../../services/errorMessagesService"

function AddCachePopup({ OnActionClose }) {
  const dispatch = useDispatch();
  const snackBar = useSnackbar();
  const [trigger, setTrigger] = useState(true);
  const selectedCache = useSelector((state) => state.cache.selectedCache);

  useEffect(() => {
    if (selectedCache) {
        dispatch(clearSelection());
    }
    if (trigger === false) {
      if (OnActionClose instanceof Function) {
        OnActionClose();
      }
    }
  }, [trigger]);

  const OnFormSubmitHandler = (formData, setErrors) => {
    const createCacheDto = {
      description: formData.description,
      lat: formData.lat,
      lon: formData.lon,
      name: formData.name,
    };

    dispatch(createCache(createCacheDto))
      .unwrap()
      .then(() => {
        snackBar.enqueueSnackbar("Cache Added Succesfully!,", {
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
      <CacheForm
        Cache={{
          name: "",
          lat: 0,
          lon: 0,
          description: "",
        }}
        OnFormSubmit={OnFormSubmitHandler}
        ButtonName="Create"
      />
    </Popup>
  );
}

export default AddCachePopup;
