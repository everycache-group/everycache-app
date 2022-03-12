import DeleteIcon from "@mui/icons-material/Delete";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import EditIcon from "@mui/icons-material/Edit";
import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useSnackbar } from "notistack";
import * as Style from "./style";
import AddCachePopup from "./../../content/CachePopup/AddCachePopup/AddCachePopup";
import EditCachePopup from "./../../content/CachePopup/EditCachePopup/EditCachePopup";
import DeleteCachePopup from "./../../content/CachePopup/DeleteCachePopup/DeleteCachePopup";
import ReviewsIcon from "@mui/icons-material/Reviews";
import RatingCommentCache from "../../content/Rating/RatingCommentCache";

function CacheMenu({ personal }) {
  const [action, setAction] = useState("");
  const selectedCache = useSelector((state) => state.cache.selectedCache);
  const currentUsername = useSelector((state) => state.user.username);
  const snackBar = useSnackbar();

  const OnClickHandler = (e) => {
    if(!personal && selectedCache.owner == currentUsername){
      snackBar.enqueueSnackbar("Can't visit own cache!", {variant: "error"});
      return;
    }

    let newAction = e.currentTarget.id;
    if (newAction === "add" || selectedCache){
      setAction(newAction);
    } else {
      snackBar.enqueueSnackbar("No cache selected for action!", {variant: "error"});
    }
  };

  const OnActionClose = () => {
    setAction("");
  };

  return (
    <Style.CacheActionContainer>
      {personal ? (
        <>
          <div onClick={OnClickHandler} id="add">
            <Style.TransformIconButton aria-label="Add Cache">
              <AddCircleOutlineIcon fontSize="medium" color="success" />
            </Style.TransformIconButton>
            {action === "add" && (
              <AddCachePopup OnActionClose={OnActionClose} />
            )}
          </div>
          <div onClick={OnClickHandler} id="edit">
            <Style.TransformIconButton aria-label="Edit Cache">
              <EditIcon fontSize="medium" color="info" />
            </Style.TransformIconButton>
            {action === "edit" && (
              <EditCachePopup OnActionClose={OnActionClose} />
            )}
          </div>
          <div onClick={OnClickHandler} id="delete">
            <Style.TransformIconButton aria-label="Delete Cache">
              <DeleteIcon fontSize="medium" color="error" />
            </Style.TransformIconButton>
            {action === "delete" && (
              <DeleteCachePopup OnActionClose={OnActionClose} />
            )}
          </div>
        </>
      ) : (
        <div onClick={OnClickHandler} id="review">
          <Style.TransformIconButton aria-label="Review Cache">
            <ReviewsIcon fontSize="medium" color="primary" />
          </Style.TransformIconButton>
          {action === "review" && (
            <RatingCommentCache OnActionClose={OnActionClose} ButtonName="Mark as visited" cacheId={selectedCache.id} />
          )}
        </div>
      )}
    </Style.CacheActionContainer>
  );
}

export default CacheMenu;
