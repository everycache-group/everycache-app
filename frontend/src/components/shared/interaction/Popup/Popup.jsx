import React, { useState, useEffect, useCallback} from "react";
import * as Style from "./style";

const Popup = ({ title, children, trigger, setTrigger }) => {
  const handlePopupClick = (e) => {
    e.stopPropagation();
  };

  const handleESC = useCallback((event) => {
    if (event.key === "Escape") {
      setTrigger(false);
    }
  }, []);

  useEffect(() => {
      document.addEventListener("keydown", handleESC, false);
      return () => {
        document.removeEventListener("keydown", handleESC, false);
      };
  }, []);

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
