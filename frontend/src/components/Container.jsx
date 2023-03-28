import Head from "next/head";
import { Navigation  } from "./Navigation";

export const Container = ({ children, className = "", title = "Books Web"}) => {
    return (
        <>
            <Head>
                <title>{title}</title>
                <meta name="description" content="Generated by create next app" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <Navigation />
            <div className={className}>
                {children}
            </div>
        </>
    )
}