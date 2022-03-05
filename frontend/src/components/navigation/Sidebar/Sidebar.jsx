import * as Style from "./style.js";
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

  const {verified: isVerified, role: userRole} = useSelector((state) => state.user);

  return (
    <>
      <IconContext.Provider value={{ }}>
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
            <SubMenu item={{
              title: "Home",
              path: "/",
              icon: <AiIcons.AiFillHome />,
            }}/>

            <SubMenu item={{
              title: "Caches",
              path: "/map",
              icon: <FaIcons.FaMap />,
            }}/>

            <SubMenu item={{
              title: "My Caches",
              path: "/mymap",
              icon: <FaIcons.FaMapMarkedAlt />,
            }}/>

            {(isVerified || userRole == "Admin") && <SubMenu item={{
              title: "Users",
              path: "/users",
              icon: <FaIcons.FaUsers />,
            }}/>}
          </Style.SidebarWrap>
        </Style.SidebarNav>
      </IconContext.Provider>
    </>
  );
}

export default Sidebar;
