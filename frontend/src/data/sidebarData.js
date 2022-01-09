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
    subNav: [
      {
        title: "SubMenu1",
        path: "/submenu1",
        icon: <AiIcons.AiFillIeSquare />,
      },
      {
        title: "SubMenu2",
        path: "/submenu2",
        icon: <AiIcons.AiFillIeSquare />,
      },
    ],
  },
  {
    title: "Map",
    path: "/map",
    icon: <FaIcons.FaMap />,
    iconClosed: iconClosed,
    iconOpened: iconOpened,
  },
  {
    title: "Next",
    path: "/next",
    icon: <AiIcons.AiFillMail />,
    iconClosed: iconClosed,
    iconOpened: iconOpened,
  },
  {
    title: "Test3",
    path: "/test3",
    icon: <AiIcons.AiFillAlipaySquare />,
    iconClosed: iconClosed,
    iconOpened: iconOpened,
  },
];
