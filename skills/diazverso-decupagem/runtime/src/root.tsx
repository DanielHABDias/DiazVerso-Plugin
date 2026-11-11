import React from 'react';
import {Composition} from 'remotion';
import {SmokeScene} from './smoke-scene';
import {HQMigrationScene} from './hq-migration-scene';
import {I04NoxScene} from './i04-nox-scene';
import {IntegratedScene} from './integrated-scene';

/** G05/H09 independent TSX sandbox, no external Content Lab dependencies.
 * Both output aspect ratios use one real Remotion composition implementation.
 */
export const Root:React.FC = () => <>
  <Composition id="DiazversoIntegratedWide" component={IntegratedScene}
    durationInFrames={600} fps={30} width={1920} height={1080}
    defaultProps={{plan:null}}/>
  <Composition id="DiazversoIntegratedShort" component={IntegratedScene}
    durationInFrames={405} fps={30} width={1080} height={1920}
    defaultProps={{plan:null}}/>
  <Composition id="DiazversoI04NoxVertical" component={I04NoxScene}
    durationInFrames={240} fps={30} width={1080} height={1920}/>
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
  <Composition
    id="DiazversoHQMigrationWide"
    component={HQMigrationScene}
    durationInFrames={60} fps={30} width={1920} height={1080}/>
  <Composition
    id="DiazversoHQMigrationVertical"
    component={HQMigrationScene}
    durationInFrames={60} fps={30} width={1080} height={1920}/>
</>;
