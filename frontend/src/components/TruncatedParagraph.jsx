import { useState } from 'react';

export const TruncatedParagraph = ({ className, text, charLimit, maxSize = 40 }) => {
  const [showFullText, setShowFullText] = useState(false);

  const toggleShowFullText = () => {
    setShowFullText(!showFullText);
  };

  const truncatedText = text.length > charLimit ? text.slice(0, charLimit) + '...' : text;
  const maxSizeText = text.length > maxSize;

  return (
    <>
    {
        maxSizeText ? (<p className={className}>{showFullText ? text : truncatedText} {text.length > charLimit && (
            <a className='a-button' onClick={toggleShowFullText}>{showFullText ? 'Ver menos' : 'Ver más...'}</a>
        )}</p>) : (<h2 className={className}>{text}</h2>)
    }
    </>
  );
};

