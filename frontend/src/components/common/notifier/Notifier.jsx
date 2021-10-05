import React from 'react'
import Alert from '@mui/material/Alert';
import * as Style from './style';

function Notifier({message}) {
    return (
        <Style.NotifierWrapper>   
            <Alert variant="filled" severity="error">
                {message}
            </Alert>
        </Style.NotifierWrapper>
    )
}

export default Notifier
