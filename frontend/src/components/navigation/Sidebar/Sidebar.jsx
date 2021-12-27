import * as Style from "./style.js";
import { SideBarData } from "./../../../data/sidebarData";
import React, { useState, useEffect } from "react";
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
import SubMenu from "../Submenu/Submenu.jsx";
import { IconContext } from "react-icons/lib";
import UserBar from "../UserBar/UserBar.jsx";
import { toggleSidebar } from "../../../redux/slices/navigationSlice";
import { useDispatch, useSelector } from "react-redux";

function Sidebar(props) {
  const sidebar = useSelector((state) => state.navigation.sidebarVisible);
  const dispatch = useDispatch();

  const showSidebar = () => {
    dispatch(toggleSidebar(!sidebar));
  };

  return (
    <>
      <IconContext.Provider value={{ color: "#fff" }}>
        <Style.Nav>
          <Style.NavIcon to="#">
            <FaIcons.FaBars onClick={showSidebar} />
          </Style.NavIcon>
          <UserBar />
        </Style.Nav>

        <Style.SidebarNav sidebar={sidebar}>
          <Style.SidebarWrap>
            <Style.NavIcon to="#">
              <AiIcons.AiOutlineClose onClick={showSidebar} />
            </Style.NavIcon>
            {SideBarData.map((item, index) => {
              return <SubMenu item={item} key={index} />;
            })}
          </Style.SidebarWrap>
        </Style.SidebarNav>
      </IconContext.Provider>
    </>
  );
}

export default Sidebar;
