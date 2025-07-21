import { Canvas, useFrame } from '@react-three/fiber';
import { useGLTF } from '@react-three/drei';
import React, { useRef } from 'react';
import * as THREE from 'three';

function LeavesModel() {
  const gltf = useGLTF('/leaves.glb');
  const ref = useRef<THREE.Group>(null);

  useFrame(() => {
    if (ref.current) {
      // ref.current.rotation.x = Math.PI / 2 * -1;
      ref.current.rotation.x = Math.PI / 2 * -1;
      ref.current.rotation.z += 0.003;
      ref.current.rotation.y = 0.3;
    }
  });

  return (
    <primitive
      ref={ref}
      object={gltf.scene}
      scale={35}
    />
  );
}

export const Background3D: React.FC = () => (
  <div
    style={{
      position: 'fixed',
      inset: 0,
      zIndex: -1,
      pointerEvents: 'none',
      width: '100vw',
      height: '100vh',
      overflow: 'hidden',
    }}
  >
    <Canvas
      camera={{ position: [0, 0, 30], fov: 50 }}
      style={{ width: '100vw', height: '100vh', background: 'transparent' }}
      gl={{ alpha: true }}
    >
      <ambientLight intensity={0.7} />
      <directionalLight position={[5, 5, 5]} intensity={0.7} />
      <LeavesModel />
    </Canvas>
  </div>
);

useGLTF.preload('/leaves.glb'); 