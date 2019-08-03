import React from 'react';
import ReactMapGL, {NavigationControl, ViewState} from 'react-map-gl';
import {ReactNode, useEffect, useState} from "react";

const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN || '';


// interface State {
//     viewport: ViewState
// }

interface MapProps {
    children?: ReactNode
    height?: number | string
    width?: number | string
}

const FullScreenMap = (props: MapProps) => {
    // A full-screen map widget

    const initialState = {
        viewport: {
            latitude: 31.7683,
            longitude: 35.2137,
            zoom: 8,
            height: props.height || 200,
            width: props.width || 200,
        },
    };

    type State = typeof initialState
    const [state, setState] = useState<State>(initialState);

    // Register the resize event listener with useEffect
    // Pass in a function to execute when the component finishes mounting
    // Return from the pass-in function another function to execute when the component unmounts
    useEffect(
        () => {
        window.addEventListener('resize', resize);
        resize();
        // Return from the first function argument another function, which will be called during unmount
        return () => window.removeEventListener('resize', resize);
        },

    );

    const updateViewport = (viewport: ViewState) => {
        setState(prevState => ({
            viewport: { ...prevState.viewport, ...viewport },
        }));
    };

    const resize = () => {
        setState(prevState => ({
            viewport: {
                ...prevState.viewport,
                height: window.innerHeight,
                width: window.innerWidth,
            },
        }));
    };

    return (
        <ReactMapGL
            {...state.viewport}
            mapboxApiAccessToken={MAPBOX_TOKEN}
            onViewportChange={(v: ViewState) => updateViewport(v)}
        >
            <div style={{ position: 'absolute', right: 30, bottom: 30 }}>
               <NavigationControl onViewportChange={updateViewport} />
            </div>
            {props.children}
        </ReactMapGL>
    );
};

export default FullScreenMap;