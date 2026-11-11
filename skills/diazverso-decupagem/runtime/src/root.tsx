import React from 'react';
import {Composition} from 'remotion';
import {SmokeScene} from './smoke-scene';

/** H09 integration sandbox: entirely synthetic. No real clips, audio,
 * uploads, external Content Lab, or licensed third-party media.
 */
export const Root:React.FC = () => <Composition
  id="DiazversoSmoke" component={SmokeScene}
  durationInFrames={60} fps={30} width={1080} height={1920}
  defaultProps={{title:'Diazverso — teste independente'}}/>;
