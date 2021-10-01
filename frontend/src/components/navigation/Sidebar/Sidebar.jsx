import * as Style from './style.js'
import { SideBarData } from './../../../data/sidebarData'
import React, { useState } from 'react'
import * as FaIcons from 'react-icons/fa'
import * as AiIcons from 'react-icons/ai'
import SubMenu from '../Submenu/Submenu.jsx'
import { IconContext } from 'react-icons/lib'
import {callAPI} from './../../../api/api-caller'


function Sidebar(props) {
    const [sidebar, setSidebar] = useState(true);

    const showSidebar = () => setSidebar(!sidebar);

    callAPI('GET', 'caches').then(x => console.log(x)).catch(x => console.log(x));

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
                           
                            return <SubMenu item={item} key={index} />
                        })}
                    </Style.SidebarWrap>
                </Style.SidebarNav>
            </IconContext.Provider>
        </>
    )
}

export default Sidebar;
