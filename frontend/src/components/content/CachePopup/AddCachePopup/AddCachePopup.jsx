import React, { useState, useEffect } from "react";
import Popup from "./../../../shared/interaction/Popup/Popup";
import CacheForm from "../../cacheForm/CacheForm";
import { createCache } from "./../../../../redux/slices/cacheSlice";
import { useDispatch } from "react-redux";
import { useSnackbar } from "notistack";

function AddCachePopup({ OnActionClose }) {
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

  const OnFormSubmitHandler = (formData) => {
    const createCacheDto = {
      description: formData.description,
      lat: formData.lat,
      lon: formData.lng,
      name: formData.name,
    };

    dispatch(createCache(createCacheDto)).then(({ meta }) => {
      console.log(meta.requestStatus);
      snackBar.enqueueSnackbar("Cache Added Succesfully!,", {
        variant: "success",
      });
      setTrigger(false);
      OnActionClose();
    });
  };

  return (
    <Popup trigger={trigger} setTrigger={setTrigger}>
      <CacheForm
        Cache={{
          name: "",
          lat: 0,
          lng: 0,
          description: "",
        }}
        OnFormSubmit={OnFormSubmitHandler}
        ButtonName="Create"
      />
    </Popup>
  );
}

export default AddCachePopup;
