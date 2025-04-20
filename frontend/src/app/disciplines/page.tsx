"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

const PresentationPage = () => {
  const router = useRouter();
  useEffect(() => {
    router.back();
  }, []);
  return <div>error</div>;
};

export default PresentationPage;
