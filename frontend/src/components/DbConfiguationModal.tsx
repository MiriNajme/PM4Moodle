import { DotsVerticalIcon } from "@radix-ui/react-icons";
import { Button, Dialog, Flex, Text, TextField } from "@radix-ui/themes";
import React, { useCallback, useEffect, useState } from "react";
import { getDbConfig, saveDbConfig, type DbConfigModel } from "../services";
import Spinner from "./ui/Spinner";

const DbConfiguationModal = React.memo(() => {
  const [dbConfig, setDbConfig] = useState<DbConfigModel>({
    host: "localhost",
    port: 3306,
    user: "root",
    password: "",
    db_name: "moodle",
  });

  const [isLoading, setLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setDbConfig((prevConfig) => ({
      ...prevConfig,
      [name]: value,
    }));
  }, []);

  const handleSubmit = useCallback(
    async (e: React.MouseEvent) => {
      e.preventDefault();
      setIsSaving(true);

      try {
        await saveDbConfig(dbConfig);
      } catch (err) {
        console.error("Error setting database configuration:", err);
      } finally {
        setIsSaving(false);
      }
    },
    [dbConfig]
  );

  useEffect(() => {
    const fetchDbConfig = async () => {
      setLoading(true);
      try {
        const config = await getDbConfig();
        setDbConfig(config);
      } catch (err) {
        console.error("Error fetching database configuration:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDbConfig();
  }, []);

  return (
    <Dialog.Root>
      <Dialog.Trigger>
        <Button
          variant='ghost'
          color='gray'
          aria-label='Database configuration'
          title='Database configuration'
        >
          <DotsVerticalIcon />
        </Button>
      </Dialog.Trigger>

      <Dialog.Content maxWidth='450px'>
        <Dialog.Title>Database configuration</Dialog.Title>
        <Dialog.Description size='2' mb='4'>
          Update your moodle database configuration.
        </Dialog.Description>

        {isLoading && <Spinner />}
        {!isLoading && (
          <>
            <Flex direction='column' gap='3'>
              <label>
                <Text as='div' size='2' mb='1' weight='bold'>
                  Host
                </Text>
                <TextField.Root
                  name='host'
                  defaultValue={dbConfig.host}
                  placeholder='ex: localhost'
                  onChange={handleChange}
                />
              </label>
              <label>
                <Text as='div' size='2' mb='1' weight='bold'>
                  Port
                </Text>
                <TextField.Root
                  defaultValue={dbConfig.port.toString()}
                  name='port'
                  placeholder='3306'
                  onChange={handleChange}
                />
              </label>
              <label>
                <Text as='div' size='2' mb='1' weight='bold'>
                  User
                </Text>
                <TextField.Root
                  defaultValue={dbConfig.user}
                  name='user'
                  placeholder='sa'
                  onChange={handleChange}
                />
              </label>
              <label>
                <Text as='div' size='2' mb='1' weight='bold'>
                  Password
                </Text>
                <TextField.Root
                  defaultValue={dbConfig.password}
                  name='password'
                  type='password'
                  placeholder='your db password'
                  onChange={handleChange}
                />
              </label>
              <label>
                <Text as='div' size='2' mb='1' weight='bold'>
                  Database name
                </Text>
                <TextField.Root
                  defaultValue={dbConfig.db_name}
                  name='db_name'
                  placeholder='moodle'
                  onChange={handleChange}
                />
              </label>
            </Flex>

            <Flex gap='3' mt='4' justify='end'>
              <Dialog.Close>
                <Button variant='soft' color='gray'>
                  Cancel
                </Button>
              </Dialog.Close>
              <Dialog.Close>
                <Button loading={isSaving} onClick={handleSubmit}>
                  Save
                </Button>
              </Dialog.Close>
            </Flex>
          </>
        )}
      </Dialog.Content>
    </Dialog.Root>
  );
});

export default DbConfiguationModal;
