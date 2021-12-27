import React from "react";
import * as Style from "./style";
import { useSelector } from "react-redux";

function PageWrapper(props) {
  const sidebarVisible = useSelector(
    (state) => state.navigation.sidebarVisible
  );

  return (
    <Style.PageWrapper sidebar={sidebarVisible}>
      {props.children}
    </Style.PageWrapper>
  );
}

export default PageWrapper;
