import React from "react";
import * as FaIcons from "react-icons/fa";
import * as AiIcons from "react-icons/ai";
//import * as IoIcons from 'react-icons/io'
import * as RiIcons from "react-icons/ri";

// Description -> use this file to add new menu with icon and path to route

const iconClosed = <RiIcons.RiArrowDownSFill />;
const iconOpened = <RiIcons.RiArrowUpSFill />;

export const SideBarData = [
  {
    title: "Home",
    path: "/",
    icon: <AiIcons.AiFillHome />,
    iconClosed: iconClosed,
    iconOpened: iconOpened,
  },
  {
    title: "My Caches",
    path: "/mymap",
    icon: <FaIcons.FaMap />,
    iconClosed: iconClosed,
    iconOpened: iconOpened,
  },
  {
    title: "Caches",
    path: "/map",
    icon: <FaIcons.FaMap />,
  },
  {
    title: "Users",
    path: "/users",
    icon: <FaIcons.FaMap />,
    iconClosed: iconClosed,
    iconOpened: iconOpened,
  }
];
