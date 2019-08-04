import React, {useRef} from 'react';
import ReactMapGL, {NavigationControl, ViewState} from 'react-map-gl';
import {ReactNode, useEffect, useState} from "react";
import {BoxProps, Text, Box, Flex} from "rebass";
import {TLengthStyledSystem} from "styled-system";

const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN || '';


// interface State {
//     viewport: ViewState
// }

interface MapProps extends BoxProps {
    children?: ReactNode
    width?: TLengthStyledSystem
    height?: TLengthStyledSystem
}

const Map = (props: MapProps) => {
    // A full-screen map widget

    const initialState = {
        viewport: {
            latitude: 31.7683,
            longitude: 35.2137,
            zoom: 8,
            height: props.height || '100%',
            width: props.width || '100%'
        },
    };

    type State = typeof initialState
    const [state, setState] = useState<State>(initialState);
    const divRef = useRef<HTMLDivElement>(null);

    // Register the resize event listener with useEffect
    // Pass in a function to execute when the component finishes mounting
    // Return from the pass-in function another function to execute when the component unmounts
    useEffect(
        () => {
            const resize = () => {
                setState(prevState => ({
                    viewport: {
                        ...prevState.viewport,
                        height: divHeight() || state.viewport.height,
                        width: divWidth() || state.viewport.width,
                    },
                }));
            };
            window.addEventListener('resize', resize);
            resize();
            // Return from the first function argument another function, which will be called during unmount
            return () => window.removeEventListener('resize', resize);
        },
        []
    );

    const updateViewport = (viewport: ViewState) => {
        setState(prevState => ({
            viewport: { ...prevState.viewport, ...viewport },
        }));
    };

    const divHeight = () => {
        if (divRef && divRef.current) {
            return divRef.current.clientHeight
        }
    };

    const divWidth = () => {
        if (divRef && divRef.current) {
            return divRef.current.clientWidth
        }
    };

    return (
        <div ref={divRef}>
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
        </div>
    );
};

export default Map;