import {
  DownloadIcon,
  MinusIcon,
  PlusIcon,
  ResetIcon,
} from "@radix-ui/react-icons";
import { Button } from "@radix-ui/themes";
import { useCallback, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";

export default function ImagePreview() {
  const [params] = useSearchParams();

  const [scale, setScale] = useState(1);
  const [isDragging, setIsDragging] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [startDrag, setStartDrag] = useState<{ x: number; y: number } | null>(
    null
  );

  const imageUrl = useMemo(() => params.get("url") ?? "", [params]);

  const imageStyle = useMemo(
    () => ({
      transform: `scale(${scale}) translate(${position.x / scale}px, ${
        position.y / scale
      }px)`,
      transformOrigin: "center",
      width: "100%",
      height: "100%",
      cursor: scale > 1 ? (isDragging ? "grabbing" : "grab") : "default",
    }),
    [scale, position, isDragging]
  );

  const handleMouseDown = useCallback(
    (e: React.MouseEvent<HTMLImageElement>) => {
      if (scale === 1) return;
      setIsDragging(true);
      setStartDrag({ x: e.clientX - position.x, y: e.clientY - position.y });
    },
    [scale, position]
  );

  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      if (!isDragging || !startDrag) return;
      setPosition({
        x: e.clientX - startDrag.x,
        y: e.clientY - startDrag.y,
      });
    },
    [isDragging, startDrag]
  );

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
    setStartDrag(null);
  }, []);

  const handleZoomIn = useCallback(() => {
    setScale((prev) => Math.min(prev * 1.2, 3)); // Limit max zoom to 3x
  }, []);

  const handleZoomOut = useCallback(() => {
    setScale((prev) => Math.max(prev / 1.2, 0.5)); // Limit min zoom to 0.5x
  }, []);

  const handleResetZoom = useCallback(() => {
    setScale(1);
    setPosition({ x: 0, y: 0 });
  }, []);

  const handleDownload = useCallback(async () => {
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
  }, [imageUrl]);

  return (
    <div className='relative w-full min-h-[95dvh] bg-gray-50 py-10 px-6 rounded-lg shadow-xl overflow-auto'>
      <img
        src={imageUrl}
        alt='Preview'
        style={imageStyle}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
      />

      <div className='fixed bottom-16 right-16 w-max flex gap-2 p-2 bg-white rounded-lg shadow-lg'>
        <Button
          size='2'
          variant='soft'
          color='gray'
          title='Zoom in'
          onClick={handleZoomIn}
        >
          <PlusIcon />
        </Button>

        <Button
          size='2'
          variant='soft'
          color='gray'
          title='Zoom out'
          onClick={handleZoomOut}
        >
          <MinusIcon />
        </Button>

        <Button
          size='2'
          variant='soft'
          color='gray'
          title='Reset zoom'
          onClick={handleResetZoom}
        >
          <ResetIcon />
        </Button>

        <Button
          size='2'
          variant='soft'
          color='gray'
          title='Download'
          onClick={handleDownload}
        >
          <DownloadIcon />
        </Button>
      </div>
    </div>
  );
}
