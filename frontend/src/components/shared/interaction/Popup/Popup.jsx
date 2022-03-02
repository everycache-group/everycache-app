import React, { useState } from "react";
import * as Style from "./style";

const Popup = ({ title, children, trigger, setTrigger }) => {
  const handlePopupClick = (e) => {
    e.stopPropagation();
  };

  return trigger ? (
    <Style.Popup onClick={handlePopupClick}>
      <Style.PopupInner>
        <Style.TitleText variant="h5">{title}</Style.TitleText>
        <Style.CloseIcon size={25} onClick={() => setTrigger(false)} />
        {children}
      </Style.PopupInner>
    </Style.Popup>
  ) : (
    ""
  );
};

export default Popup;
