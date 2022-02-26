import React, { useState, useEffect } from "react";
import Popup from "./../../../shared/interaction/Popup/Popup";
import CacheForm from "../../cacheForm/CacheForm";
import { updateCache } from "./../../../../redux/slices/cacheSlice";
import { useDispatch, useSelector } from "react-redux";
import { selector } from "react-redux";
import { useSnackbar } from "notistack";

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

  const OnFormSubmitHandler = (formData) => {
    const updateCacheDto = {
      id: selectedCache.id,
      description: formData.description,
      lat: formData.lat,
      lon: formData.lng,
      name: formData.name,
    };

    dispatch(updateCache(updateCacheDto)).then(({ meta }) => {
      console.log(meta.requestStatus);
      snackBar.enqueueSnackbar("Cache Updated Succesfully!,", {
        variant: "info",
      });
      setTrigger(false);
      OnActionClose();
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
