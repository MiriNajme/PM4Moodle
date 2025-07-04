import { DownloadIcon, ExternalLinkIcon } from "@radix-ui/react-icons";
import {
  Button,
  Flex,
  Grid,
  Heading,
  Inset,
  Popover,
  Text,
} from "@radix-ui/themes";

export function ImageButton({
  imageUrl,
  buttonText,
  title,
  description,
  buttonIcon,
  onClick,
}: {
  imageUrl: string;
  buttonText?: string;
  title: string;
  description: string;
  buttonIcon: React.ReactNode;
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
    <Popover.Root>
      <Popover.Trigger>
        <Button variant='soft'>
          {buttonIcon}
          {buttonText}
        </Button>
      </Popover.Trigger>
      <Popover.Content width='360px'>
        <Grid columns='130px 1fr'>
          <Inset side='left' pr='current'>
            <img
              src={
                imageUrl ??
                "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?&auto=format&fit=crop&w=400&q=80"
              }
              style={{ objectFit: "cover", width: "100%", height: "100%" }}
              onError={(e) => {
                (e.target as HTMLImageElement).src =
                  "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?&auto=format&fit=crop&w=400&q=80";
              }}
            />
          </Inset>

          <div>
            <Heading size='2' mb='1'>
              {title}
            </Heading>
            <Text as='p' size='2' mb='4' color='gray'>
              {description}
            </Text>

            <Flex direction='column' align='stretch' gap='2'>
              <Popover.Close>
                <Button size='1' variant='soft' onClick={onClick}>
                  <ExternalLinkIcon width='16' height='16' />
                  view in full size
                </Button>
              </Popover.Close>
              <Popover.Close>
                <Button size='1' variant='soft' onClick={handleDownload}>
                  <DownloadIcon width='16' height='16' />
                  Download
                </Button>
              </Popover.Close>
            </Flex>
          </div>
        </Grid>
      </Popover.Content>
    </Popover.Root>
  );
}
