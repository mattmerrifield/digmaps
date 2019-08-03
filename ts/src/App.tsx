import React from 'react';
import logo from './logo.svg';
import './App.css';
import {Box, Flex, Text} from "rebass";

const App: React.FC = () => {
  return (
    <Flex
        className="App"
    >
        <Flex
            bg={'black'}
            flexDirection={'column'}
        >
            <Flex
                bg={'orange'}
                flexDirection={'row'}
                justifyContent={'center'}
            >
                <Text>Header</Text>
            </Flex>

            <Flex
                flexDirection={'row'}
            >
                <Box
                    width={1/5}
                    bg={'blue'}
                >
                    <Text>Left</Text>
                </Box>
                <Box width={3/5} bg={'white'}>
                    <Text>Center</Text>
                </Box>
                <Box width={1/5} bg={'red'}>
                    <Text>Right</Text>
                </Box>
            </Flex>

            <Flex
                bg={'green'}
                flexDirection={'row'}
                justifyContent={'center'}
            >
                <Text>
                    Footer
                </Text>
            </Flex>
        </Flex>
    </Flex>
  );
};

export default App;
