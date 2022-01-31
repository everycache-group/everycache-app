import React, { useState } from "react";
import * as Style from "./style";

const Popup = ({ children, trigger, setTrigger }) => {
  const handlePopupClick = (e) => {
    e.stopPropagation();
  };

  const [open, setOpen] = useState(!!trigger); //convert any value to boolean

  return open ? (
    <Style.Popup onClick={handlePopupClick}>
      <Style.PopupInner>
        <Style.CloseIcon size={25} onClick={() => setOpen(false)} />
        {children}
      </Style.PopupInner>
    </Style.Popup>
  ) : (
    ""
  );
};

export default Popup;
