import DeleteIcon from "@mui/icons-material/Delete";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import EditIcon from "@mui/icons-material/Edit";
import React, { useState } from "react";
import * as Style from "./style";
import AddCachePopup from "./../../content/CachePopup/AddCachePopup/AddCachePopup";
import EditCachePopup from "./../../content/CachePopup/EditCachePopup/EditCachePopup";
import DeleteCachePopup from "./../../content/CachePopup/DeleteCachePopup/DeleteCachePopup";

function CacheMenu() {
  const [action, setAction] = useState("");

  const OnClickHandler = (e) => {
    setAction(e.currentTarget.id);
  };

  const OnActionClose = () => {
    setAction("");
  };

  return (
    <Style.CacheActionContainer>
      <div onClick={OnClickHandler} id="add">
        <Style.TransformIconButton aria-label="Add Cache">
          <AddCircleOutlineIcon fontSize="medium" color="success" />
        </Style.TransformIconButton>
        {action === "add" && <AddCachePopup OnActionClose={OnActionClose} />}
      </div>
      <div onClick={OnClickHandler} id="edit">
        <Style.TransformIconButton aria-label="Edit Cache">
          <EditIcon fontSize="medium" color="info" />
        </Style.TransformIconButton>
        {action === "edit" && <EditCachePopup OnActionClose={OnActionClose} />}
      </div>
      <div onClick={OnClickHandler} id="delete">
        <Style.TransformIconButton aria-label="Delete Cache">
          <DeleteIcon fontSize="medium" color="error" />
        </Style.TransformIconButton>
        {action === "delete" && (
          <DeleteCachePopup OnActionClose={OnActionClose} />
        )}
      </div>
    </Style.CacheActionContainer>
  );
}

export default CacheMenu;
