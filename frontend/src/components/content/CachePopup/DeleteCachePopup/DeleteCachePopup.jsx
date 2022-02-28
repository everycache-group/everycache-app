import React, { useEffect, useState } from "react";
import Popup from "../../../shared/interaction/Popup/Popup";
import Button from "@mui/material/Button";
import { Typography } from "@mui/material";
import * as Style from "./style";
import { useDispatch, useSelector } from "react-redux";
import { deleteCache } from "./../../../../redux/slices/cacheSlice";
import { useSnackbar } from "notistack";

function DeleteCachePopup({ OnActionClose }) {
  const [trigger, setTrigger] = useState(true);

  useEffect(() => {
    if (trigger === false) {
      if (OnActionClose instanceof Function) {
        OnActionClose();
      }
    }
  }, [trigger]);

  const snackBar = useSnackbar();
  const dispatch = useDispatch();
  const selectedCache = useSelector((state) => state.cache.selectedCache);

  const OnDeleteHandler = (e) => {
    dispatch(deleteCache(selectedCache.id))
      .then(() => {
        snackBar.enqueueSnackbar("Cache Deleted Succesfully!", {
          variant: "success",
        });
        setTrigger(false);
        OnActionClose();
      })
      .catch((error) => {
        snackBar.enqueueSnackbar("Cache couldn't be deleted. Try Again.,", {
          variant: "error",
        });
      });
  };

  return (
    <Popup title="Delete Cache" trigger={trigger} setTrigger={setTrigger}>
      <Style.PopupContainer>
        <Typography variant="h6" display="block">
          Are you sure you want to delete
          <br /> this cache?
        </Typography>
        <Style.ButtonContainer>
          <Button variant="contained" onClick={OnDeleteHandler}>
            Yes
          </Button>
          <Button variant="contained">Cancel</Button>
        </Style.ButtonContainer>
      </Style.PopupContainer>
    </Popup>
  );
}

export default DeleteCachePopup;
