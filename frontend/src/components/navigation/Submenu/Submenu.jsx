import React, { useState } from "react";
import * as Style from "./style.js";

const SubMenu = ({ item }) => {
  const [subNav, setSubNav] = useState(false);

  const showSubNav = (open) => setSubNav(open);

  return (
    <>
      <Style.SidebarLink
        to={item.path}
        onMouseEnter={item.subNav && (() => showSubNav(true))}
        onMouseLeave={item.subNav && (() => showSubNav(false))}
      >
        <div>
          {item.icon}
          <Style.SidebarLabel>{item.title}</Style.SidebarLabel>
        </div>
        <div>
          {item.subNav && subNav
            ? item.iconOpened
            : item.subNav
            ? item.iconClosed
            : null}
        </div>
      </Style.SidebarLink>
      <Style.DropDownLinkWrapper
        onMouseEnter={item.subNav && (() => showSubNav(true))}
        onMouseLeave={item.subNav && (() => showSubNav(false))}
        subNav={subNav}
      >
        {subNav &&
          item.subNav.map((item, index) => {
            return (
              <Style.DropDownLink to={item.path} key={index}>
                {item.icon}
                <Style.SidebarLabel>{item.title}</Style.SidebarLabel>
              </Style.DropDownLink>
            );
          })}
      </Style.DropDownLinkWrapper>
    </>
  );
};

export default SubMenu;
