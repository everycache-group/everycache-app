import React from 'react'
import Notifier from '../components/common/notifier/Notifier'


function useNotifier({message, ...rest}) {
    return <Notifier message={message} />
}

export default useNotifier
