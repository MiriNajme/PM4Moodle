import React from "react";
import { Heading } from "@radix-ui/themes";
import DbConfigurationModal from "../components/DbConfigurationModal.tsx";
import extractorLogo from "../assets/extractor-logo3.png";

const MoodleHeading = React.memo(() => {
  return (
    <Heading as='h1' size='6' className='flex flex-col items-center mb-8 pb-8'>
      <span className='flex items-center justify-between w-full'>
        <span className='flex items-center'>
          <img
            src={extractorLogo}
            alt='Extractor Logo'
            className='inline-block w-32 h-32 mr-4'
          />
          <span className='text-3xl font-bold'>PM4Moodle</span>
        </span>
        <DbConfigurationModal />
      </span>
    </Heading>
  );
});

export default MoodleHeading;
