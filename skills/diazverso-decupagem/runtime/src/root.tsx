import React from 'react';
import {Composition} from 'remotion';
import {SmokeScene} from './smoke-scene';

/** G05/H09 independent TSX sandbox, no external Content Lab dependencies.
 * Both output aspect ratios use one real Remotion composition implementation.
 */
export const Root:React.FC = () => <>
  <Composition
    id="DiazversoSmoke"
    component={SmokeScene}
    durationInFrames={60} fps={30} width={1080} height={1920}
    defaultProps={{title:'Diazverso — teste vertical independente'}}/>
  <Composition
    id="DiazversoSmokeWide"
    component={SmokeScene}
    durationInFrames={60} fps={30} width={1920} height={1080}
    defaultProps={{title:'Diazverso — teste horizontal independente'}}/>
</>;
