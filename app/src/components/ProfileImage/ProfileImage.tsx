import Image from "next/image";

type ProfileImageProps = {
  src: string;
  alt: string;
};

export default function ProfileImage({ src, alt }: ProfileImageProps) {
  // TODO: provide a default profile image when no profile image provided?
  // This may not be a concern if we only support Oauth providers.

  return (
    <div>
      <Image
        src={
          src ??
          "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
        }
        alt={alt}
        width={40}
        height={40}
        className="rounded-full"
      />
    </div>
  );
}
