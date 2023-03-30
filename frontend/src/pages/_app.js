import 'bootswatch/dist/sketchy/bootstrap.min.css'
import '@/styles/globals.css'
import { useEffect } from 'react'

export default function App({ Component, pageProps }) {

  useEffect(() => {
    require('bootstrap'); 
  })

  return <Component {...pageProps} />
}
