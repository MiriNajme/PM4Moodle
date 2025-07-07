import { DownloadIcon, ExternalLinkIcon } from "@radix-ui/react-icons";
import { Button, Flex, Heading, Text } from "@radix-ui/themes";
import coverPng from "../../assets/JSON-OCEL.png";

export function ImageButton({
  imageUrl,
  title,
  description,
  isJson = false,
  onClick,
}: {
  imageUrl: string;
  title: string;
  description: string;
  isJson: boolean;
  onClick?: () => void;
}) {
  const handleDownload = async () => {
    try {
      const response = await fetch(imageUrl, { mode: "cors" });
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.download = imageUrl.endsWith(".png")
        ? "ocel-dfg.png"
        : "ocel-dfg.json";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch {
      alert("Failed to download image. This may be due to CORS restrictions.");
    }
  };

  return (
    <div className='max-w[480px] w-full rounded-lg shadow-lg p-4'>
      <div className='grid grid-cols-[130px_1fr] gap-4'>
        <div>
          <img
            src={isJson ? coverPng : imageUrl ?? coverPng}
            className='w-30 h-full object-cover rounded-lg'
          />
        </div>
        <div>
          <Heading size='2' mb='1'>
            {title}
          </Heading>
          <Text as='p' size='2' mb='4' color='gray'>
            {description}
          </Text>

          <Flex direction='column' align='stretch' gap='2'>
            <Button size='1' variant='soft' onClick={onClick}>
              <ExternalLinkIcon width='16' height='16' />
              View in full size
            </Button>
            <Button size='1' variant='soft' onClick={handleDownload}>
              <DownloadIcon width='16' height='16' />
              Download
            </Button>
          </Flex>
        </div>
      </div>
    </div>
  );
}
