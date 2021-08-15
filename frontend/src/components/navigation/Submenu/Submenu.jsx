import React, { useState } from 'react'
import * as Style from './style.js';

const SubMenu = ({item}) => {
    const[subNav, setSubNav] = useState(false);

    const showSubNav = () => setSubNav(!subNav);

    return (
        <>
            <Style.SidebarLink to={item.path} onClick={item.subNav && showSubNav}>
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
            {
                subNav && item.subNav.map((item, index) => {
                return (
                    <Style.DropDownLink to={item.path} key={index} >
                        {item.icon} 
                        <Style.SidebarLabel>{item.title}</Style.SidebarLabel> 
                    </Style.DropDownLink>
                )
            })}
            
        </>
    );
};

export default SubMenu;