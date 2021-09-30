import * as Style from './style.js'
import { SideBarData } from './../../../data/sidebarData'
import React, { useState } from 'react'
import * as FaIcons from 'react-icons/fa'
import * as AiIcons from 'react-icons/ai'
import SubMenu from '../Submenu/Submenu.jsx'
import { IconContext } from 'react-icons/lib'
import {callAPI} from './../../../api/url-resolver';

function Sidebar(props) {
    const [sidebar, setSidebar] = useState(true);

    const showSidebar = () => setSidebar(!sidebar);

    return (
        <>
            <IconContext.Provider value={{ color: '#fff'}}>
                <Style.Nav>
                    <Style.NavIcon to='#'> 
                        <FaIcons.FaBars onClick={showSidebar} />
                    </Style.NavIcon>
                </Style.Nav>

                <Style.SidebarNav sidebar={sidebar}>
                    <Style.SidebarWrap>
                        <Style.NavIcon to='#' >
                            <AiIcons.AiOutlineClose onClick={showSidebar}/>
                        </Style.NavIcon>
                        {SideBarData.map((item, index) => {
                            console.log(createURL());
                            return <SubMenu item={item} key={index} />
                        })}
                    </Style.SidebarWrap>
                </Style.SidebarNav>
            </IconContext.Provider>
        </>
    )
}

export default Sidebar;
